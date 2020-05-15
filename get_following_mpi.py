import twint, json
from mpi4py import MPI
import pandas as pd

def get_accounts(path = ''):
    data = pd.read_csv(path+'twitter_accounts.csv')
    sub_data = data.dropna()
    print('number of valid accounts', sub_data.shape[0], 'out of', data.shape[0])
    accounts = list(sub_data[sub_data['to_check_following']>30]['twitter'])
    return accounts


def get_following_id(tid):
    print('start search following id,', tid)
    c = twint.Config()
    c.Username = tid
    c.Store_object = True
    c.User_full = True
    c.Hide_output = True
    twint.run.Following(c)
    target_users = twint.output.users_list
    
    user_info = []
    for user in target_users:
        add = dict()
        try:
            add['handle'] = user.username
            add['name'] = user.name
            add['bio'] = user.bio
            add['url'] = user.url
            add['join_date'] = user.join_date
            add['location'] = user.location
            add['num_tweets'] = user.tweets
            add['num_followers'] = user.followers
            add['num_following'] = user.following
            #add['verified'] = user.verified
        except AttributeError: print(user.username); pass
        user_info.append(add)
    
    return {tid: user_info}


def test(tid):
    return {'a': tid}


def run_all():
    accounts = get_accounts()[1:11]
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    #temp_result = get_following_id(accounts[rank])
    temp_result = test(accounts[rank])

    if rank == 0: result = [None for i in range(len(accounts))]
    comm.Gather(sendbuf = loc_result, recvbuf = result, root=0)
    json.dump(result, open('twint_following.json', 'a'))

    return


def main():
    run_all()

    

if __name__ == '__main__':
    main()
