import requests
import re
from urllib import parse

POSTHEADERS = {'Host': 'twitter.com',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Referer': 'https://twitter.com/',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Content-Length': 0,
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}

USERAGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}

Session = requests.session()


class LoginFailure(Exception):
    pass


class AlreadyTweeted(Exception):
    pass


class TwitterClient(object):

    def change_url(self, url):
        data = {
            'authenticity_token': self.Token,
            'page_context': 'me',
            'section_context': 'profile',
            'user[url]': url
                }

        response = Session.post('https://twitter.com/i/profiles/update',
                                headers=POSTHEADERS,
                                data=data,
                                allow_redirects=False)

        if 'user_url' in response.text:
            return True

        return False

    def change_location(self, loc):

        data = {
            'authenticity_token': self.Token,
            'page_context': 'me',
            'section_context': 'profile',
            'user[location]': loc
        }

        response = Session.post('https://twitter.com/i/profiles/update',
                                headers=POSTHEADERS,
                                data=data)

        if 'Thanks, your settings have been saved.' in response.text:
            return True
        
        return False

    def change_description(self, desc):

        data = {
                'authenticity_token': self.Token,
                'page_context': 'me',
                'section_context': 'profile',
                'user[description]': desc
            }

        response = Session.post('https://twitter.com/i/profiles/update',
                                headers=POSTHEADERS,
                                data=data)

        if 'Thanks, your settings have been saved.' in response.text:
            return True

        return False

    def change_username(self, newusername):

        data = {
                '_method': 'PUT',
                'authenticity_token': self.Token,
                'user[screen_name]': newusername,
                'auth_password': self.Password
                }

        response = Session.post('https://twitter.com/settings/accounts/update',
                                data=data,
                                headers=POSTHEADERS)

        if 'Thanks, your settings have been saved.' in response.text:
            return True
            
        return False

    def get_followings(self, link, follower=True):

        links = []
        followers = []

        if not follower:
            link = 'https://mobile.twitter.com/{0}/following'.format(link)
        else:
            link = 'https://mobile.twitter.com/{0}/followers'.format(link)

        links.append(link)
        source = requests.get(link).text

        while 'Show more people' in source:

            patt = re.compile(r'<div class="w-button-more"><a href="(.*?)">Show more people</a></div>', re.MULTILINE)
            nextPage = re.search(patt, source).group(1)
            nextPage = 'https://mobile.twitter.com' + nextPage
            source = requests.get(nextPage).text
            links.append(nextPage)

        for a in links:
            Source = requests.get(a).text
            pattern = re.compile(r'<a href="/(.*?)"><span class="username"><span>@</span>(.*?)</span></a>',
                                 re.MULTILINE)

            for a in re.findall(pattern, Source):
                followers.append('https://www.twitter.com/' + a[1])

        return followers

    def change_email(self, email):

        data = {'_method': 'PUT',
                'authenticity_token': self.Token,
                'user[screen_name]': self.Account,
                'user[email]': email,
                'auth_password': self.Password}

        response = Session.post('https://twitter.com/settings/accounts/update',
                                data=data,
                                headers=POSTHEADERS)

        if 'A message has been sent to you to confirm your new email address.' in response.text:
            return True

        return False

    def direct_message(self, user, message):

        data = {'authenticity_token': self.Token,
                'lastMsgId': '',
                'screen_name': user,
                'scribeContext[component]': 'dm_existing_conversation_dialog',
                'text': message}

        response = Session.post('https://twitter.com/i/direct_messages/new', data=data, headers=POSTHEADERS)

        if message in response.text:
            return True

        return False

    def delete_tweet(self, tweet):
        
        tweet = tweet.split('/')[5]

        data = {'_method': 'DELETE',
                'authenticity_token': self.Token,
                'id': tweet}

        response = Session.post('https://twitter.com/i/tweet/destroy',
                                data=data, headers=POSTHEADERS,
                                allow_redirects=False)
 
        if 'Your tweet has been deleted.' in response.text:
            return True

        return False

    def fav(self, tweet, delete=False):

        tweet = tweet.split('/')[5]

        if delete:
            url = 'https://twitter.com/i/tweet/unfavorite'
        else:
            url = 'https://twitter.com/i/tweet/favorite'

        data = {'authenticity_token': self.Token,
                'id': tweet
                }

        response = Session.post(url, headers=POSTHEADERS, data=data)

        if 'Favorited 1 time' in response.text:
            return True
        else:
            return False

    def follow(self, user, follow = True):

        if not follow:
            url = 'https://twitter.com/i/user/unfollow'
        else:
            url = 'https://twitter.com/i/user/follow'

        request = Session.get('https://www.twitter.com/{0}'.format(user))

        userID = re.search('<div class="ProfileNav" role="navigation" data-user-id="(.*?)">', request.text).group(1)

        data = {'authenticity_token': self.Token,
                'challenges_passed': 'false',
                'handles_challenges': '1',
                'inject_tweet': 'false',
                'user_id': userID}

        response = Session.post(url, headers=POSTHEADERS, data=data)

        if response.status_code == 200:
            return True

        return False 

    def get_trends(self):#Login not required

        request = requests.get('https://mobile.twitter.com/trends')
        trends = []
        pattern = re.compile('<a href=\"/search(.*?)">\n(.*?)\n')

        for match in re.findall(pattern, request.text):
            a = match[1]
            a = a.strip()
            trends.append(a)

        return trends

    def retweet(self, tweet, delete=False):

        tweet = tweet.split('/')[5]

        if delete:
            url = "https://twitter.com/i/tweet/unretweet"
        else:
            url = 'https://twitter.com/i/tweet/retweet'

        data = {'authenticity_token': self.Token,
                'id': tweet
                }

        response = Session.post(url, headers=POSTHEADERS, data=data)

        if 'Tweets' in response.text:
            return True

        return False

    def tweet(self, message, reply = False, statusID = str):

        data = {'authenticity_token': self.Token,
                'place_id': '',
                'tagged_users': ''
        }

        if reply:
            user = statusID.split('/')[3]
            statusID = statusID.split('/')[5]
            data.update({'in_reply_to_status_id':statusID})
            message = '@{0} '.format(user + message)
            data.update({'status': message})

        else:
            data.update({'status': message})

        response = Session.post('https://twitter.com/i/tweet/create', data=data, headers=POSTHEADERS)

        errmsg = 'You have already sent this Tweet.'
        if errmsg in response.text:
            raise AlreadyTweeted('You already tweeted that!')
        if response.status_code == 200:
            return True

        return False

    def login(self, account, password):

        account = account.lower()

        request = Session.get('https://www.twitter.com/',
                              headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                       'Host': 'twitter.com'})

        self.Account = account
        self.Password = password
        self.Token = re.search('<input type="hidden" value="(.*?)" name="authenticity_token">', request.text).group(1)

        data = parse.urlencode({

            'authenticity_token': parse.quote(self.Token),
            'redirect_after_login': '/',
            'scribe_log': '',
            'return_to_ssl': 'true',
            'session[password]': parse.quote(self.Password),
            'session[username_or_email]': parse.quote(self.Account),
            })

        response = Session.post('https://www.twitter.com/sessions', headers=POSTHEADERS, data=data)

        pageSource = response.text.lower()

        if 'user-style-' + self.Account in pageSource:
            print("Auth Token: %s" % self.Token)
            return True
        else:
            raise LoginFailure('Login failed check password/username')