  import path from 'node:path'
  
  export function example8(): string {
      const filePath: string = path.join(__dirname, "example_008.ts");
    const fileContents = 42
    return fileContents
//  ^^^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2322] Type 'number' is not assignable to type 'string'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import path from 'node:path'
// DIFF   
// DIFF   export function example8(): string {
// DIFF       const filePath: string = path.join(__dirname, "example_008.ts");
// DIFF -  	const fileContents = 42
// DIFF -  	return fileContents
// DIFF +  	const fileContents = fs.readFileSync(filePath, 'utf8');
// DIFF +  	return fileContents;
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2304] Cannot find name 'fs'.

  }
  
