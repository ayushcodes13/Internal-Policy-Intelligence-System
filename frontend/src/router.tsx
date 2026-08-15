import { Outlet, createRootRoute, createRoute } from "@tanstack/react-router";
import { HomePage } from "./screens/home";

const rootRoute = createRootRoute({
  component: () => <Outlet />
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: HomePage
});

export const routeTree = rootRoute.addChildren([indexRoute]);
