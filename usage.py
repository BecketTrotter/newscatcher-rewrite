from newscatcher import Newscatcher


nc = Newscatcher('seekingalpha.com', 'finance')
ret = nc.search(25)
print(len(ret['articles']))