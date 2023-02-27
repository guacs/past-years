import { HopeProvider } from "@hope-ui/solid";
import { Router, useRoutes } from "@solidjs/router";

import Header from "./layout/Header";
import routes from "./routes";
import themeConfig from "./theme";

const Routes = useRoutes(routes);

export default function App() {
	return (
		<HopeProvider config={themeConfig}>
			<Router>
				<Header />
				<Routes />
			</Router>
		</HopeProvider>
	);
}
