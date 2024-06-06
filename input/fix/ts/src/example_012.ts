import makeWebAuthn from 'webauthn4js'

export function example12()  {
	return makeWebAuthn({
		RPDisplayName: 'WebAuthnJS',
		RPID: 'localhost',
		RPOrigins: [`https://localhost:${port}`],
		AuthenticatorSelection: {
			userVerification: 'preferred'
		}
	});
}
