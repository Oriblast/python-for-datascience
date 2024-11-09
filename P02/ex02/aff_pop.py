import matplotlib.pyplot as plt
from load_csv import load

def aff_pop(pop_str):
    """
    en realité cette fonction va enlevé le M ou le K pour et les remplacer par leurs valeurs 
    10⁹ pour le and 10³ for k
    just for true calcul
    """
    if pop_str.endswith("M"):
        return float(pop_str[:-1]) * 1e6
    elif pop_str.endswith("k"):
        return float(pop_str[:-1]) * 1e3
    else:
        return float(pop_str)

def main():
    """
        load the file csv and well
    """
    data = load("population_total.csv")

    campus = "Belgium"
    country = "France"

    Belgium_data = data[data['country'] == campus].iloc[:, 1:]
    france_data = data[data['country'] == country].iloc[:, 1:]

    Belgium_pop = Belgium_data.values.flatten()
    france_pop = france_data.values.flatten()
    years = Belgium_data.columns.astype(int) + 1

    Belgium_pop = [aff_pop(pop) for pop in Belgium_pop]
    france_pop = [aff_pop(pop) for pop in france_pop]

    plt.plot(years, Belgium_pop, label=campus)
    plt.plot(years, france_pop, label=country, color='green')

    plt.title("Population in {} and {}".format(campus, country))
    plt.xlabel("Year")
    plt.xticks(range(1800, 2051, 40))
    plt.tight_layout()
    plt.ylabel("Population")
    plt.legend(loc="lower right")
    plt.tight_layout()
    max_pop = max(max(Belgium_pop), max(france_pop))
    i = 1
    y_ticks = [i * 1e7 * 2 for i in range(1 ,int(max_pop / 1e7) - 2)]
    plt.yticks(y_ticks, ["{:,.0f}M".format(pop / 1e6) for pop in y_ticks])
    #plt.yticks(ticks=[20 * 1e6, 40 * 1e6, 60 * 1e6], labels=['20M', '40M', '60M'])
    plt.show()
if __name__ == "__main__":
    main()
