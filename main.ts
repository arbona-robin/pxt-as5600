/**
 * Custom blocks for AS5600 Magnetic Rotary Encoder
 */
//% weight=100 color=#0fbc11 icon="\uf021"
namespace AS5600 {
    const AS5600_ADDRESS = 0x36;
    const STATUS_REGISTER = 0x0B;
    const ANGLE_REGISTER_H = 0x0E; // Registre pour les bits de poids fort de l'angle

    /**
     * Reads the status of the magnet from the sensor.
     * @returns The status byte from the sensor.
     */
    function getStatus(): number {
        // Spécifier le registre de statut
        let reg = pins.createBuffer(1);
        reg[0] = STATUS_REGISTER;
        pins.i2cWriteBuffer(AS5600_ADDRESS, reg);

        // Lire 1 octet de données
        let data = pins.i2cReadBuffer(AS5600_ADDRESS, 1);
        return data[0];
    }

    /**
     * Reads the rotation angle from the AS5600 sensor.
     * @returns The angle in degrees (0-360).
     */
    //% block="lire l'angle en degrés"
    export function readAngle(): number {
        // Spécifier le registre d'angle
        let reg = pins.createBuffer(1);
        reg[0] = ANGLE_REGISTER_H;
        pins.i2cWriteBuffer(AS5600_ADDRESS, reg);

        // Lire 2 octets de données
        let data = pins.i2cReadBuffer(AS5600_ADDRESS, 2);

        // Combiner les deux octets pour obtenir la valeur de l'angle (0-4095)
        let angle = (data[0] << 8) | data[1];

        // Convertir en degrés
        let degrees = (angle * 360) / 4096;
        return degrees;
    }

    /**
     * Checks if a magnet is detected by the sensor.
     * @returns True if a magnet is detected, false otherwise.
     */
    //% block="aimant détecté"
    export function isMagnetDetected(): boolean {
        let status = getStatus();
        // Vérifie le 5ème bit (MD)
        return (status & 0b00100000) != 0;
    }

    /**
     * Checks if the magnet is too weak.
     * @returns True if the magnet is too weak, false otherwise.
     */
    //% block="aimant trop faible"
    export function isMagnetTooWeak(): boolean {
        let status = getStatus();
        // Vérifie le 4ème bit (ML)
        return (status & 0b00010000) != 0;
    }

    /**
     * Checks if the magnet is too strong.
     * @returns True if the magnet is too strong, false otherwise.
     */
    //% block="aimant trop fort"
    export function isMagnetTooStrong(): boolean {
        let status = getStatus();
        // Vérifie le 3ème bit (MH)
        return (status & 0b00001000) != 0;
    }
}