  import makeWebAuthn from 'webauthn4js'
  
  export function example13()  {
   return makeWebAuthn({
   	RPDisplayName: 'WebAuthnJS',
   	PID: 'localhost',
//  ^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2561] Object literal may only specify known properties, but 'PID' does not exist in type 'Config'. Did you mean to write 'RPID'?

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import makeWebAuthn from 'webauthn4js'
// DIFF   
// DIFF   export function example13()  {
// DIFF   	return makeWebAuthn({
// DIFF   		RPDisplayName: 'WebAuthnJS',
// DIFF - 		PID: 'localhost',
// DIFF + 		RPID: 'localhost',
// DIFF   		RPOrigins: ["https://localhost:8080"],
// DIFF   		AuthenticatorSelection: {
// DIFF   			userVerification: 'preferred'
// DIFF   		}
// DIFF   	});
// DIFF   }
// DIFF   

   	RPOrigins: ["https://localhost:8080"],
   	AuthenticatorSelection: {
   		userVerification: 'preferred'
   	}
   });
  }
  
