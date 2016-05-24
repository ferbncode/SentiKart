class Senti():
    def take_review(rev):
        soup = BeautifulSoup(rev)
        print(soup.findAll