__author__ = 'zou'


# No need to process files and manipulate strings - we will
# pass in lists (of equal length) that correspond to
# sites views. The first list is the site visited, the second is
# the user who visited the site.

# See the test cases for more details.

def highest_affinity(site_list, user_list, time_list):
    # Returned string pair should be ordered by dictionary order
    # I.e., if the highest affinity pair is "foo" and "bar"
    # return ("bar", "foo").
    site_dict = dict()
    for i in range(0, len(site_list)):
        if site_list[i] in site_dict:
            if user_list[i] in site_dict[site_list[i]]:
                pass
            else:
                site_dict[site_list[i]].add(user_list[i])
        else:
            site_dict[site_list[i]] = {user_list[i]}

    count = 0
    l = []
    for d1 in site_dict:
        for d2 in site_dict:
            if d1 != d2 and len(site_dict[d1] & site_dict[d2]) > count:
                del l[:]
                l = [d1, d2]
                count = len(site_dict[d1] & site_dict[d2])

    return tuple(sorted(l))
