from sqids import Sqids

def generate_short_url(url: str) -> str:
    sqids = Sqids(min_length=3)
    return sqids.encode(url)

if __name__=='__main__':
    a = generate_short_url("https://github.com/sqids/sqids-python")
    print(a)