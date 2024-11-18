import sys


def ft_tqdm(lst: range) -> None:
    """
    Mimic tqdm function using the yield operator.
    """
    # Nombre total d'éléments
    total = len(lst)
    for i, item in enumerate(lst):
        # Calculer le pourcentage de progression
        progress = int((i + 1) / total * 100)
        # Afficher la barre de progression
        bar = '=' * (progress // 2) + '>' + ' ' * (50 - (progress // 2))
        sys.stdout.write(f'\r{progress}%|[{bar}]| {i + 1}/{total}')
        sys.stdout.flush()
        yield item
