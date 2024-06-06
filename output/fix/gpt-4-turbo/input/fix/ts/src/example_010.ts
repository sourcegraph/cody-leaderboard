  import fs from 'node:fs'
  import path from 'node:path'
  
  export function example10(): string {
      const filePath: string = path.join(__dirname, "example.ts");
    const fileContents = 42
    return fileContents
//  ^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2322] Type 'number' is not assignable to type 'string'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import fs from 'node:fs'
// DIFF   import path from 'node:path'
// DIFF   
// DIFF   export function example10(): string {
// DIFF       const filePath: string = path.join(__dirname, "example.ts");
// DIFF -  	const fileContents = 42
// DIFF -  	return fileContents
// DIFF +  	const fileContents = fs.readFileSync(filePath, 'utf8');
// DIFF +  	return fileContents;
// DIFF   }
// DIFF   

  }
  
