/** Capitalizes the first letter of each word in a given string.
 *
 * @param s - The string to titlify.
 */
export function title(s: string): string {
	// TODO: Try to make this more efficient.
	const words = s.toLowerCase().split(" ");
	const capitalizedWords = words.map(
		(w) => w[0].toUpperCase() + w.substring(1),
	);
	return capitalizedWords.join(" ");
}
