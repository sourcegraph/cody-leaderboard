  import { sum } from './example_004-import'
  
  export function example4(): number {
   return sum(41, "bananas is 42. I like the motorcycles honda and yamaha")
//                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2345] Argument of type 'string' is not assignable to parameter of type 'Summer'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import { sum } from './example_004-import'
// DIFF   
// DIFF   export function example4(): number {
// DIFF - 	return sum(41, "bananas is 42. I like the motorcycles honda and yamaha")
// DIFF + 	return sum(41, 42)
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2345] Argument of type 'number' is not assignable to parameter of type 'Summer'.

  }
  
