import * as React from "react";
import AppShell from "../components/atoms/AppShell";
import { Box, Heading, Text } from "grommet";

const IndexPage = () => {
  return (
    <AppShell>
      <Box>
        <Text>Nav Option</Text>
      </Box>
      <div>
        <h1>Khoj documentation</h1>
        <Text size={"medium"}>
          A multimodal multilingual search engine framework
        </Text>
      </div>
    </AppShell>
  );
};

export default IndexPage;
