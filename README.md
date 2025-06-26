# Extension MakeCode pour AS5600

Cette extension pour Microsoft MakeCode permet d'utiliser le capteur d'angle magnétique rotatif AS5600 avec la carte micro:bit.

## Blocs

L'extension fournit les blocs suivants :

*   `lire l'angle en degrés`: Lit l'angle actuel du capteur en degrés (0-360).
*   `aimant détecté`: Vérifie si un aimant est détecté par le capteur.
*   `aimant trop faible`: Vérifie si le champ magnétique de l'aimant est trop faible.
*   `aimant trop fort`: Vérifie si le champ magnétique de l'aimant est trop fort.

## Utilisation

Pour utiliser cette extension, ajoutez-la à votre projet MakeCode en utilisant l'URL du dépôt GitHub : `https://github.com/arbona-robin/pxt-as5600`

Voici un exemple simple qui affiche l'angle sur la matrice de LEDs :

```typescript
basic.forever(function () {
    let angle = AS5600.readAngle()
    basic.showNumber(angle)
})
```

## Licence

MIT
