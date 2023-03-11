import {
	Anchor,
	Box,
	Divider,
	Flex,
	Heading,
	IconButton,
	Spacer,
	useColorMode,
} from "@hope-ui/solid";
import { A } from "@solidjs/router";
import { FaSolidMoon } from "solid-icons/fa";
import { IoSunnyOutline } from "solid-icons/io";

export default function Header() {
	// TODO: Get a logo for this somehow.
	return (
		<>
			<Flex as="nav" alignItems="center" p={10}>
				<Heading p="$3" size={{ "@md": "3xl", "@initial": "3xl" }}>
					<Anchor
						as={A}
						href="/"
						_hover={{
							textDecoration: "none",
							cursor: "pointer",
						}}
					>
						Past
						<Box as={"span"} color="$accent10">
							Quest
						</Box>
					</Anchor>
				</Heading>
				<Heading p="$3" size={{ "@md": "3xl", "@initial": "xl" }}>
					<Anchor
						_hover={{
							textDecoration: "none",
							cursor: "pointer",
						}}
						as={A}
						href="/questions"
					>
						PYQs
					</Anchor>
				</Heading>
				<Spacer />
				<DarkModeToggle />
			</Flex>
			<Divider color="$accent10" />
		</>
	);
}

function DarkModeToggle() {
	const { colorMode, toggleColorMode } = useColorMode();

	const getIcon = () =>
		colorMode() === "light" ? <FaSolidMoon /> : <IoSunnyOutline />;

	return (
		<IconButton
			onClick={toggleColorMode}
			variant="ghost"
			colorScheme="neutral"
			aria-label="Toggle dark/light mode"
			icon={getIcon()}
			_focus={{
				boxShadow: "none",
			}}
		/>
	);
}
