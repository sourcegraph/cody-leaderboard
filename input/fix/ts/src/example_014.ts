import makeWebAuthn from 'webauthn4js'

export function example14()  {
	return makeWebAuthn({
		RPDisplayName: 'WebAuthnJS',
		HostResolver: 'localhost',
		Timeouts: 422,
		RPOrigins: ["https://localhost:8080"],
		AuthenticatorSelection: {
			userVerification: 'preferred'
		}
	});
}
