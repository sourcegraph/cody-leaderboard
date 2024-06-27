package rockskip

import (
	"bytes"
	"context"
	"fmt"
	"sort"
	"strings"
	"testing"

	"github.com/google/go-cmp/cmp"
	"github.com/stretchr/testify/require"

	"github.com/sourcegraph/sourcegraph/internal/api"
	"github.com/sourcegraph/sourcegraph/internal/database/dbtest"
	"github.com/sourcegraph/sourcegraph/internal/gitserver"
	"github.com/sourcegraph/sourcegraph/internal/search"
)

func TestIndex(t *testing.T) {
	repo, repoDir := gitserver.MakeGitRepositoryAndReturnDir(t)
	// Needed in CI
	gitRun(t, repoDir, "config", "user.email", "test@sourcegraph.com")

	git, err := newSubprocessGit(t, repoDir)
	require.NoError(t, err)
	defer git.Close()

	db, service := mockService(t, git)
	defer db.Close()

	state := map[string][]string{}
	verifyBlobs := func() {
		out, err := gitserver.CreateGitCommand(repoDir, "git", "rev-parse", "HEAD").CombinedOutput()
		require.NoError(t, err, string(out))
		commit := string(bytes.TrimSpace(out))

		args := search.SymbolsParameters{
			Repo:         repo,
			CommitID:     api.CommitID(commit),
			Query:        "",
			IncludeLangs: []string{"Text"}}
		symbols, err := service.Search(context.Background(), args)
		require.NoError(t, err)

		// Make sure the paths match.
		gotPathSet := map[string]struct{}{}
		for _, blob := range symbols {
			gotPathSet[blob.Path] = struct{}{}
		}
		gotPaths := []string{}
		for gotPath := range gotPathSet {
			gotPaths = append(gotPaths, gotPath)
		}
		wantPaths := []string{}
		for wantPath := range state {
			// We only want .txt files since we're filtering by lang: text
			if strings.Contains(wantPath, ".txt") {
				wantPaths = append(wantPaths, wantPath)
			}
		}
		sort.Strings(gotPaths)
		sort.Strings(wantPaths)
		if diff := cmp.Diff(gotPaths, wantPaths); diff != "" {
			fmt.Println("unexpected paths (-got +want)")
			fmt.Println(diff)
			err = PrintInternals(context.Background(), db)
			require.NoError(t, err)
			t.FailNow()
		}

		gotPathToSymbols := map[string][]string{}
		for _, blob := range symbols {
			gotPathToSymbols[blob.Path] = append(gotPathToSymbols[blob.Path], blob.Name)
		}

		// Make sure the symbols match.
		for gotPath, gotSymbols := range gotPathToSymbols {
			wantSymbols := state[gotPath]
			sort.Strings(gotSymbols)
			sort.Strings(wantSymbols)
			if diff := cmp.Diff(gotSymbols, wantSymbols); diff != "" {
				fmt.Println("unexpected symbols (-got +want)")
				fmt.Println(diff)
				err = PrintInternals(context.Background(), db)
				require.NoError(t, err)
				t.FailNow()
			}
		}
	}

	gitAdd(t, repoDir, state, "a.txt", "sym1\n")
	verifyBlobs()

	gitAdd(t, repoDir, state, "b.txt", "sym1\n")
	verifyBlobs()

	gitAdd(t, repoDir, state, "c.txt", "sym1\nsym2")
	verifyBlobs()

	gitAdd(t, repoDir, state, "a.java", "sym1\nsym2")
	verifyBlobs()

	gitAdd(t, repoDir, state, "a.txt", "sym1\nsym2")
	verifyBlobs()

	gitRm(t, repoDir, state, "a.txt")
	verifyBlobs()
}