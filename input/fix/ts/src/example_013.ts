import makeWebAuthn from 'webauthn4js'

export function example13()  {
	return makeWebAuthn({
		RPDisplayName: 'WebAuthnJS',
		PID: 'localhost',
		RPOrigins: ["https://localhost:8080"],
		AuthenticatorSelection: {
			userVerification: 'preferred'
		}
	});
}
