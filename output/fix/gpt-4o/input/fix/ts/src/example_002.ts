  import type { Example2 } from "./example_002-import";
  
  export function example2(): Example2 {
   const example2: Example2 = "something is 42";
//       ^^^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2322] Type 'string' is not assignable to type 'Example2'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import type { Example2 } from "./example_002-import";
// DIFF   
// DIFF   export function example2(): Example2 {
// DIFF - 	const example2: Example2 = "something is 42";
// DIFF + 	const example2: Example2 = { something: 42 };
// DIFF   	return example2;
// DIFF   }
// DIFF   

   return example2;
  }
  
