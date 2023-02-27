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
	return (
		<>
			<Flex as="nav" alignItems="center" m={10} p={10}>
				<Heading p="$3" size={{ "@md": "5xl", "@initial": "3xl" }}>
					<Anchor as={A} href="/">
						CSE
					</Anchor>
				</Heading>
				<Box>
					<Heading p="$3" size={{ "@md": "3xl", "@initial": "xl" }}>
						<Anchor as={A} href="/questions">
							PYQs
						</Anchor>
					</Heading>
				</Box>
				<Spacer />
				<DarkModeToggle />
			</Flex>
			<Divider />
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
