import {
  Audio,
  Code,
  lines,
  Img,
  Video,
  LezerHighlighter,
  makeScene2D,
  word,
} from "@revideo/2d";
import { all, chain, createRef, waitFor, useScene } from "@revideo/core";
import { parser } from "@lezer/javascript";
import { parser as Pyparser } from "@lezer/python";

interface CodeExplanation {
  code: string;
  Explanation: ExplanationItem[];
}

interface ExplanationItem {
  highlight: string;
  narration: string;
  duration: number;
  audio: string;
}

function escapeRegexSpecialChars(str: string): string {
  // Check if the string is already escaped
  const alreadyEscaped = str.replace(/\\\\[.*+?^${}()|[\]\\]/g, "") === "";

  if (alreadyEscaped) {
    return str;
  } else {
    // If not, escape it
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
  }
}

export default makeScene2D(function* (view) {
  const test = useScene().variables.get("lesson", {})() as CodeExplanation;
  const audioRef = createRef<Audio>();

  LezerHighlighter.registerParser(parser);
  LezerHighlighter.registerParser(Pyparser);
  const code = createRef<Code>();
  const audioNode = createRef<Audio>();

  view.add(
    <>
      <Code
        ref={code}
        offset={-1}
        position={view.size().scale(-0.5).add(60)}
        fontFamily={"Fira Code, monospace"}
        fontSize={25}
        code={test.code}
      />
      ,
    </>
  );

  for (let i = 0; i < test.Explanation.length; i++) {
    view.add(<Audio src={test.Explanation[i].audio} play={true} />);

    yield* all(
      code().selection(
        code().findFirstRange(
          escapeRegexSpecialChars(test.Explanation[i].highlight)
        ),
        0.6
      ),
      waitFor(test.Explanation[i].duration + 1)
    );
  }
});
