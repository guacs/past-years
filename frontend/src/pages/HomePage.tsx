import {
	Box,
	Button,
	Center,
	Flex,
	Grid,
	GridItem,
	Heading,
	SimpleGrid,
	Text,
} from "@hope-ui/solid";
import { useNavigate } from "@solidjs/router";

import { FaSolidArrowRight } from "solid-icons/fa";

export default function HomePage() {
	const navigate = useNavigate();

	return (
		<>
			<Flex
				flexDirection="column"
				justifyContent="center"
				alignItems="center"
				marginLeft="$20"
				marginRight="$20"
				css={{
					minH: "calc(100vh - 80px)",
				}}
				_hover={{
					cursor: "default",
				}}
			>
				<Heading
					maxW="$containerLg"
					fontWeight="$extrabold"
					css={{
						fontSize: "$3xl",
						"@md": {
							fontSize: "$8xl",
						},
					}}
				>
					Learn from the{" "}
					<Box
						as={"span"}
						css={{
							color: "$accent10",
							transition: "color 0.5s",
							_hover: {
								color: "$accent12",
							},
						}}
					>
						past
					</Box>
					.
				</Heading>
				<Text
					fontSize={{ "@initial": "$lg", "@md": "$2xl" }}
					fontFamily="$sans"
					fontWeight="$semibold"
				>
					Unlock your success with previous year's questions - Learn, Practice,
					Succeed!
				</Text>
				<Button
					size="xl"
					fontSize="5xl"
					marginTop="$7"
					marginBottom="$5"
					colorScheme="accent"
					compact
					onClick={() => navigate("/questions")}
				>
					Start Learning
				</Button>
			</Flex>
		</>
	);
}
