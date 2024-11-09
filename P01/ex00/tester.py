from give_bmi import give_bmi, apply_limit

height = [2.71, 1.15]
weight = [165.3, 38.4]

# Calcul des valeurs de l'IMC (BMI)
bmi = give_bmi(height, weight)
print(bmi, type(bmi))

# Application d'une limite pour déterminer si l'IMC est au-dessus du seuil
result = apply_limit(bmi, 26)
print(result)
