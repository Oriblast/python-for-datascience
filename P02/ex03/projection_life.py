from load_csv import load
import matplotlib.pyplot as plt


def main():
    """
    loading file and charging data 
    """
    income_data = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    if income_data.empty:
        print(f"Erreur : Aucune donnée trouvée.")
        return

    life_expectancy_data = load("life_expectancy_years.csv")
    if life_expectancy_data.empty:
        print(f"Erreur : Aucune donnée trouvée.")
        return

    year_1900_column = '1900'
    gnp_1900 = income_data[year_1900_column]
    life_expectancy_1900 = life_expectancy_data[year_1900_column]

    plt.figure(figsize=(10, 6))
    plt.scatter(gnp_1900, life_expectancy_1900)
    plt.title("Life expectancy vs Gross domestic product (Year 1900)")
    plt.xlabel("Gross domestic product")
    plt.ylabel("Life expectancy (Years)")
    plt.xscale("log")
    plt.xticks(ticks=[300, 1000, 10000], labels=['300', '1k', '10k'])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()