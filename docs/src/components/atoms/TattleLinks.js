import { Link } from "gatsby";
import React from "react";
import styled from "styled-components";

const ThemedLink = styled(Link)`
  text-decoration: "none";
  box-shadow: "none";
  background-color: "red";
  :visited {
    color: inherit;
    text-decoration: "none";
  }
`;

const ThemedPlainLink = styled(Link)`
  text-decoration: none;
  color: inherit;
  :visited {
    color: inherit;
  }
  &:hover {
    text-decoration: underline;
  }
  &.active {
    color: red;
  }
`;

const ThemedPlainHeavyLink = styled(Link)`
  font-family: "Bitter";
  font-weight: "900";
  color: inherit;
  :visited {
    color: inherit;
  }
  &:hover {
    text-decoration: none;
  }
  &.active {
    color: red;
  }
`;

const ThemedExternalLink = styled.a`
  font-weight: "bold";
  text-decoration: none;
  :visited {
  }
`;

const ThemedPlainExternalLink = styled.a`
  text-decoration: none;
  color: #514e80;
  :visited {
    color: #514e80;
    text-decoration: none;
  }
`;

const SmartPlainLink = ({ linktype, target, children }) =>
  linktype === "external" ? (
    <ThemedPlainExternalLink href={target} target={"_blank"}>
      {children}
    </ThemedPlainExternalLink>
  ) : (
    <ThemedPlainLink to={target}>{children}</ThemedPlainLink>
  );

export {
  ThemedLink as Link,
  ThemedPlainLink as PlainLink,
  ThemedPlainHeavyLink as PlainHeavyLink,
  ThemedExternalLink as ExternalLink,
  ThemedPlainExternalLink as PlainExternalLink,
  SmartPlainLink,
};
