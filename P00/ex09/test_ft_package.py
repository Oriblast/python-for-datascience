from ft_package import count_in_list

def test_count_in_list():
    assert count_in_list(["toto", "tata", "toto"], "toto") == 2
    assert count_in_list(["toto", "tata", "toto"], "tutu") == 0

if __name__ == "__main__":
    test_count_in_list()
    print("All tests passed.")
