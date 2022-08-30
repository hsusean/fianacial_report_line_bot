from imgurpython import ImgurClient
from datetime import datetime

client_id = '4cba34ef37164c5'
client_secret = '57fa8a889a895bb2ee4f0d80db4b5581afb449af'

client = ImgurClient(client_id, client_secret)

# authorization_url = client.get_auth_url('pin')
# print(111, authorization_url)
# https://api.imgur.com/oauth2/authorize?client_id=4cba34ef37164c5&response_type=pi
# credentials = client.authorize('80f3b93966', 'pin')
# # a = client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
# print(credentials)

access_token ='f1543b940f4cccefd81f57158e258bfa888d5c5f'
refresh_token= 'b746be69672c2e18e63353f857b2199828658bb4'

# {'access_token': 'f1543b940f4cccefd81f57158e258bfa888d5c5f', 'expires_in': 315360000, 'token_type': 'bearer', 'scope': None, 'refresh_token': 'b746be69672c2e18e63353f857b2199828658bb4', 'account_id': 165138265, 'account_username': 'hsusean1219'}

def upload(file_path, album='jCvv6NM' , name = 'test-name!' ,title = 'test-title' ):
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album':  album,
        'name': name,
        'title': title,
        'description': f'test-{datetime.now()}'
    }

    print("Uploading image... ")
    image = client.upload_from_path(file_path, config=config, anon=False)
    print("Done")

    return image['link']

if __name__ == '__main__':
    image = upload('C:\\Users\\User\\Pictures\\ohtani.jpg', 'jCvv6NM')
    print(image)