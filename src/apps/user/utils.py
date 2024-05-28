import random, string

# Genera un nombre aleaotorio de 30 caracteres
def generateRandomName(name, k=30) -> str:
    formatImage = get_format_image(name)
    if  formatImage != None:
        # Tomo letras mayus y minus y las sumo más números,
        # creando con random.choices 30 caracteres (k)
        nameRandom = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
        return f'{nameRandom}.{formatImage}' 
    else:
        return None

def get_format_image(name):
    typesFiles = ['jpg', 'png', 'jpeg']
    for typeFile in typesFiles:
        if typeFile in name:
            return typeFile
    return None