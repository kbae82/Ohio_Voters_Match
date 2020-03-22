class Voter:
    def __init__(self, row, name, birth_year, address, city, state, zip, matched_voterid = None):
        self.row = int(row) if row.isdigit() else None
        self.name = name.strip() if isinstance(name, str) else ''
        self.birth_year = int(birth_year) if birth_year.isdigit() else None
        self.address = address.strip() if isinstance(address, str) else ''
        self.city = city.strip() if isinstance(city, str) else ''
        self.state = state.strip() if isinstance(state, str) else ''
        self.zip = int(zip) if zip.isdigit() else None
        self.matched_voterid = matched_voterid

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __iter__(self):
        return iter([self.row, self.name, self.birth_year, self.address, self.city, self.state, self.zip, self.matched_voterid])

