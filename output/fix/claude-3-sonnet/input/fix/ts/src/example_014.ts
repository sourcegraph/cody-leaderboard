  import makeWebAuthn from 'webauthn4js'
  
  export function example14()  {
   return makeWebAuthn({
   	RPDisplayName: 'WebAuthnJS',
   	HostResolver: 'localhost',
   	Timeouts: 422,
//  ^^^^^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2322] Type 'number' is not assignable to type 'TimeoutsConfig'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import makeWebAuthn from 'webauthn4js'
// DIFF   
// DIFF   export function example14()  {
// DIFF   	return makeWebAuthn({
// DIFF   		RPDisplayName: 'WebAuthnJS',
// DIFF   		HostResolver: 'localhost',
// DIFF - 		Timeouts: 422,
// DIFF + 		Timeouts: {
// DIFF + 			pollingThrottlePeriod: 422,
// DIFF + 			pollingTimeout: 422
// DIFF + 		},
// DIFF   		RPOrigins: ["https://localhost:8080"],
// DIFF   		AuthenticatorSelection: {
// DIFF   			userVerification: 'preferred'
// DIFF   		}
// DIFF   	});
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2353] Object literal may only specify known properties, and 'pollingThrottlePeriod' does not exist in type 'TimeoutsConfig'.

   	RPOrigins: ["https://localhost:8080"],
   	AuthenticatorSelection: {
   		userVerification: 'preferred'
   	}
   });
  }
  
