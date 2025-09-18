from google_apis.Services.Gmail import Gmail


def main():
  g = Gmail()
  p = g.getMails("me","from:pinbot@explore.pinterest.com -is:starred ",False)
  idList = [m.get('id') for m in p]
  g.batchDelete("me",idList)


if __name__ == "__main__":
  main()