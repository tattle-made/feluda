import * as React from "react";
import AppShell from "../components/atoms/AppShell";
import { Box, Heading, Text } from "grommet";

// markup
const IndexPage = () => {
  return (
    <AppShell>
      <div>
        <h1>Tattle Search documentation</h1>
        <Text size={"medium"}>
          Welcome to central repository for tattle operators
        </Text>
      </div>
    </AppShell>
  );
};

export default IndexPage;
