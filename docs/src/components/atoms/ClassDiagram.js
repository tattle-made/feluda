import React from "react";
import { Box, Text } from "grommet";

const ClassDiagram = ({ name, fields, methods }) => (
  <Box
    round={"xsmall"}
    border
    pad={"small"}
    width={"fit-content"}
    margin={{ bottom: "small" }}
  >
    <Box border={"bottom"}>
      <Text size={"small"} weight={600}>
        {name}
      </Text>
    </Box>
    {fields &&
      fields.map((field) => (
        <Box>
          <Text size={"small"} weight={400}>
            {field.description
              ? field.name + " - " + field.description
              : field.name}
          </Text>
        </Box>
      ))}
    {methods &&
      methods.map((method) => (
        <Box>
          <Text size={"small"} weight={400}>
            {method.description
              ? method.name + " - " + method.description
              : method.name}
          </Text>
        </Box>
      ))}
  </Box>
);

export default ClassDiagram;
