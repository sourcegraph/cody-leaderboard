  export function example1(): number {
    return '42'
//  ^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2322] Type 'string' is not assignable to type 'number'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   export function example1(): number {
// DIFF -   return '42'
// DIFF +   return 42
// DIFF   }
// DIFF   

  }
  
