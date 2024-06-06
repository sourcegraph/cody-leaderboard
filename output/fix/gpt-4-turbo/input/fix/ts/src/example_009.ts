  import fs from 'node:fs'
  import path from 'node:path'
  
  export function example9(): string {
      const filePath: string = path.join(__dirname, "example.ts");
    const contents = fs.readFileSync(filePath, 'utf8')
    return fileContents
//         ^^^^^^^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2552] Cannot find name 'fileContents'. Did you mean 'contents'?

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import fs from 'node:fs'
// DIFF   import path from 'node:path'
// DIFF   
// DIFF   export function example9(): string {
// DIFF       const filePath: string = path.join(__dirname, "example.ts");
// DIFF    	const contents = fs.readFileSync(filePath, 'utf8')
// DIFF -  	return fileContents
// DIFF +  	return contents
// DIFF   }
// DIFF   

  }
  
