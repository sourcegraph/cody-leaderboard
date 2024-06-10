  import makeWebAuthn from 'webauthn4js'
  
  export function example11()  {
   return makeWebAuthn();
//        ^^^^^^^^^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2554] Expected 1 arguments, but got 0.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import makeWebAuthn from 'webauthn4js'
// DIFF   
// DIFF   export function example11()  {
// DIFF - 	return makeWebAuthn();
// DIFF + 	return makeWebAuthn({
// DIFF + 		// Add configuration options here
// DIFF + 	});
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2345] Argument of type '{}' is not assignable to parameter of type 'Config'.
// DIAGNOSTIC_AFTER Type '{}' is missing the following properties from type 'Config': RPID, RPDisplayName, RPOrigins

  }
  
