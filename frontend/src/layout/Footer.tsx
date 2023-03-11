import { Divider, Text, Flex, Anchor, Box } from "@hope-ui/solid";
import { Link } from "@solidjs/router";

import { FaBrandsGithub } from "solid-icons/fa";

export default function Footer() {
	/**
	 * Include the following:
	 *  - GitHub link
	 *  - link to create an issue on GitHub
	 *  - contact me directly
	 *  - logo (create one first)
	 *  - copyright with year
	 */

	return (
		<>
			<Flex flexDirection="column" justifyContent="center" paddingBottom="$5">
				<Divider />
				<Flex justifyContent="center" alignItems="center" marginTop="$3">
					<Anchor
						margin="$3"
						href="https://github.com/guacs/past-years"
						external
					>
						<FaBrandsGithub size={32} />
					</Anchor>
					<Text>
						Found a bug? Raise an issue on{" "}
						<Anchor
							textDecoration="underline"
							href="https://github.com/guacs/past-years"
						>
							GitHub
						</Anchor>
					</Text>
				</Flex>
			</Flex>
		</>
	);
}
