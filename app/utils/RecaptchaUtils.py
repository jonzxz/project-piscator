def get_recaptcha_secret() -> str:
    try:
        with open('RECAPTCHA_SECRET.key', 'r') as secret:
            key = secret.read()
            secret.close()
            return key
    except FileNotFoundError as fnfe:
        print("ReCAPTCHA secret key file not found!")
        sys.exit(1)
