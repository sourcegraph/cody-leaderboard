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
// DIFF + 		timeout: 60000,
// DIFF + 		authenticatorTimeout: 0,
// DIFF + 		requireResidentKey: false,
// DIFF + 		userVerificationMethod: 'required',
// DIFF + 		attestation: 'direct'
// DIFF + 	});
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2561] Object literal may only specify known properties, but 'timeout' does not exist in type 'Config'. Did you mean to write 'Timeout'?

  }
  
