from cryptography.hazmat.primitives.asymmetric import ed25519, x25519


def generate_identity_keypair():
    """
    Generate the long-term cryptographic identity
    for a Hermes client.

    Returns:
        signing_private,
        signing_public,
        exchange_private,
        exchange_public,
    """

    signing_private = ed25519.Ed25519PrivateKey.generate()
    signing_public = signing_private.public_key()

    exchange_private = x25519.X25519PrivateKey.generate()
    exchange_public = exchange_private.public_key()

    return (
        signing_private,
        signing_public,
        exchange_private,
        exchange_public,
    )