# Encrypts a passwords so it isn't stored as plain text
def encrypt_password(password):
    modded_password = password[::-1]
    encrypted = ""
    for i in range(len(modded_password)):
        mod_num = i + len(password)
        toggler = False
        if i % 3 == 0:
            mod_num += 9
        if i % 5 == 0:
            mod_num -= 15
        if i % 2:
            if toggler:
                mod_num += 2
                toggler = not toggler
            else:
                mod_num -= 3
                toggler = not toggler

        encrypted_char = chr(ord(modded_password[i]) + mod_num)
        encrypted += encrypted_char
    return (generate_noise(encrypted[::-1], False) + encrypted + generate_noise(encrypted[::-1], True))


# Generates noise in the password
def generate_noise(password, is_after_password):
    noise = ""
    noise_gen_range = 0
    if len(password) == 1:
        noise_gen_range = 1
    else:
        noise_gen_range = int(len(password)/2)

    for i in range(noise_gen_range):
        mod_num = i + int(len(password)/2)+i*int(len(password)/3)
        if is_after_password:
            mod_num = int(mod_num / 2)
            mod_num += 1
        toggler = False
        if i % 2 == 0:
            mod_num ^= 3
        elif i % 5 == 0:
            mod_num -= 3
        elif i % 3:
            if toggler:
                mod_num /= 2
                toggler = not toggler
            else:
                mod_num += 9
                toggler = not toggler
        elif i == 0 or i == 1:
            mod_num += (i+3)
        encrypted_char = chr(ord(password[i]) + mod_num)
        noise += encrypted_char
    return noise


# Denoises a password for decrypting
def denoise(password):
    cut_length = int(len(password)/4)
    if cut_length == 0:
        return password[1]
    return password[cut_length:-cut_length]


# Decrypts the password
def decrypt_password(password):
    modded_password = denoise(password)
    encrypted = ""
    for i in range(len(modded_password)):
        mod_num = i + len(modded_password)
        toggler = False
        if i % 3 == 0:
            mod_num += 9
        if i % 5 == 0:
            mod_num -= 15
        if i % 2:
            if toggler:
                mod_num += 2
                toggler = not toggler
            else:
                mod_num -= 3
                toggler = not toggler

        encrypted_char = chr(ord(modded_password[i]) - mod_num)
        encrypted += encrypted_char
    return encrypted[::-1]