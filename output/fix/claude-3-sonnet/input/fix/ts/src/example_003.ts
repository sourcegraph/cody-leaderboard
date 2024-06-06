  import { sum } from './example_003-import'
  
  export function example3(): number {
   return sum(40, '41', '42')
//                ^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2345] Argument of type 'string' is not assignable to parameter of type 'number'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import { sum } from './example_003-import'
// DIFF   
// DIFF   export function example3(): number {
// DIFF - 	return sum(40, '41', '42')
// DIFF + 	return sum(40, 41, 42)
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2345] Argument of type 'number' is not assignable to parameter of type 'string'.

  }
  
