import { SkeletonText, Divider } from "@hope-ui/solid";

export default function LoadingQuestion() {
	return (
		<>
			<SkeletonText mt="$10" noOfLines={4} spacing="$4" />
			<Divider marginTop="$4" marginBottom="$4" />
		</>
	);
}
