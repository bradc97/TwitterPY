import TwitterClient


def main():
    twitter = TwitterClient.TwitterClient()

    if twitter.login('username', 'password'):
        for a in ['First Tweet', 'Second','Third']:
            twitter.tweet(a, False)
    else:
        print('Sign in failed')
    
if __name__ == '__main__':
    main()
