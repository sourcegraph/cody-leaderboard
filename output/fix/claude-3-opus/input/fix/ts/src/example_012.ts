  import makeWebAuthn from 'webauthn4js'
  
  export function example12()  {
   return makeWebAuthn({
   	RPDisplayName: 'WebAuthnJS',
   	RPID: 'localhost',
   	RPOrigins: [`https://localhost:${port}`],
//                                   ^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2304] Cannot find name 'port'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import makeWebAuthn from 'webauthn4js'
// DIFF   
// DIFF   export function example12()  {
// DIFF   	return makeWebAuthn({
// DIFF   		RPDisplayName: 'WebAuthnJS',
// DIFF   		RPID: 'localhost',
// DIFF - 		RPOrigins: [`https://localhost:${port}`],
// DIFF + 		RPOrigins: [`https://localhost`],
// DIFF   		AuthenticatorSelection: {
// DIFF   			userVerification: 'preferred'
// DIFF   		}
// DIFF   	});
// DIFF   }
// DIFF   

   	AuthenticatorSelection: {
   		userVerification: 'preferred'
   	}
   });
  }
  
