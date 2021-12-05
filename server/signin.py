
def register_user(user_name: str, password: str):
    try:
        f = open('../data/logins.txt', 'a')
        f.write(f"{user_name},{password},\n")
        f.close()
        return {}
    except:
        return False

def sign_in(user_name: str, password: str):
    f = open('../data/logins.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = line.split(',')
        if line[:-1] == [user_name, password]:
            return import_ratings(line[-1])
    f.close()
    return False

def import_ratings(ratings : str) -> dict:
    # if no ratings have been given yet
    if ratings == '\n':
        return {}

    ratings_lst = ratings.strip().split('\t') # list of "movieId rating" strings
    usr_ratings = {}
    for rate in ratings_lst:
        rate = rate.split(' ') # => [movidId, rating]
        usr_ratings[int(rate[0])] = int(rate[1])

    return usr_ratings

# Export the ratings dictionary in a valid string format
def export_ratings(ratings : dict) -> str:
    final_str = ""
    for movieId in ratings.keys():
        final_str += f"{movieId} {ratings[movieId]}\t"
    return final_str + '\n'

def update_ratings(user_name: str, password: str, ratings : dict):
    f = open('../data/logins.txt', 'r')
    lines = f.readlines()
    f.close()
    
    for i in range(len(lines)):
        line = lines[i].split(',')
        
        if line[:-1] == [user_name, password]:
            lines[i] = f"{user_name},{password},{export_ratings(ratings)}"

    f = open('../data/logins.txt', 'w')
    for line in lines:
        if line != "":
            f.write(line)
    f.close()
    
    


if __name__ == '__main__':
    #register_user('jacober', 'abcd')
    test = {1:1,2:2,3:3,4:4,5:6}
    # ret = import_ratings(export_ratings(test))
    # print(ret == test)
    # register_user("tommy", "le")
    # register_user("jacober", "abcd")
    # update_ratings("jacober", "abcd", test)
    print(sign_in("jacober", "abcd"))