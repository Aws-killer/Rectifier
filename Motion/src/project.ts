import { makeProject } from "@revideo/core";
import lesson from "./variables.json";
import example from "./scenes/example?scene";

export default makeProject({
  scenes: [example],
  variables: {
    lesson: lesson,
  },
  experimentalFeatures: true,
});
