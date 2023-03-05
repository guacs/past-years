import { Box, HopeProvider } from "@hope-ui/solid";
import { Router, useRoutes } from "@solidjs/router";

import Header from "./layout/Header";
import routes from "./routes";
import themeConfig from "./theme";
import Footer from "./layout/Footer";

const Routes = useRoutes(routes);

export default function App() {
	return (
		<HopeProvider config={themeConfig}>
			<Router>
				<Header />
				<Box minH="$containerMd">
					<Routes />
				</Box>
				<Footer />
			</Router>
		</HopeProvider>
	);
}
