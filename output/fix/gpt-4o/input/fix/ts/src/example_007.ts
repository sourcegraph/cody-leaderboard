  import path from 'node:path'
  
  export function example7(): string {
   return path.resolved(process.cwd(), 'example_007.ts') 
//             ^^^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2551] Property 'resolved' does not exist on type 'PlatformPath'. Did you mean 'resolve'?

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import path from 'node:path'
// DIFF   
// DIFF   export function example7(): string {
// DIFF - 	return path.resolved(process.cwd(), 'example_007.ts')␣
// DIFF + 	return path.resolve(process.cwd(), 'example_007.ts')␣
// DIFF   }
// DIFF   

  }
  
