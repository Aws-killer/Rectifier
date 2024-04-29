import React, {useMemo} from 'react';
import {
	useVideoConfig,
	AbsoluteFill,
	TransitionSeries,
	Series,
	useCurrentFrame,
} from 'remotion';
import * as Fonts from '@remotion/google-fonts';
import transcriptData from './Assets/TextSequences.json';

function chunkArray(array, chunkSize) {
	const chunks = [];
	for (let i = 0; i < array.length; i += chunkSize) {
		chunks.push(array.slice(i, i + chunkSize));
	}
	return chunks;
}

import {TransitionSeries} from '@remotion/transitions';
const Constants = {};
const defaultText = {
	fontFamily: 'Luckiest Guy',
	fontSize: 80,
	textAlign: 'center',
	textShadow:
		'-10px -10px 0 #000, 0   -10px 0 #000, 10px -10px 0 #000, 10px  0   0 #000, 10px  10px 0 #000, 0    10px 0 #000, -10px  10px 0 #000, -10px  0   0 #000',
	position: 'fixed',
	fontWeight: 'bolder',
	color: 'yellow',
	bottom: '30vh',
	height: 'fit-content',
	width: '100%',
};
const subtitle = Constants?.text
	? {
			...defaultText,
			...Constants.text,
	  }
	: defaultText;
Fonts.getAvailableFonts()
	.filter((font) => {
		return font.fontFamily === subtitle.fontFamily;
	})[0]
	.load()
	.then((font) => font.loadFont());

const TextStream = React.memo(() => {
	const {fps} = useVideoConfig();
	const frame = useCurrentFrame();
	const memoizedTranscriptData = useMemo(() => {
		return transcriptData;
	}, []);
	const chunks = chunkArray(memoizedTranscriptData, 3);
	return (
		<AbsoluteFill
			style={{
				//backgroundColor: 'red',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<Series>
				{chunks.map((chunk, index) => {
					let delta = 0;
					if (chunk.length > 1) {
						const end = chunk[chunk.length - 1].end;
						const start = chunk[0].start;
						delta = end - start;
					} else {
						delta = chunk[0].end - chunk[0].start;
					}

					return (
						<Series.Sequence
							style={subtitle}
							key={index}
							from={delta * fps}
							durationInFrames={fps * delta}
						>
							<Letter frame={frame} style={subtitle}>
								{chunk}
							</Letter>
						</Series.Sequence>
					);
				})}
			</Series>
		</AbsoluteFill>
	);
});

const Letter = ({children, style, frame}) => {
	const {fps} = useVideoConfig();

	return (
		<div style={style} className="flex space-x-5 justify-center flex-wrap">
			{children.map((item, index) => {
				const {text, start, end} = item;
				console.log('text', text, start * fps, end * fps, frame);
				return (
					<div
						key={index}
						className=" rounded-3xl p-1"
						style={{
							backgroundColor: `${
								frame >= start * fps && frame <= end * fps
									? 'black'
									: 'transparent'
							}`,
							// fontSize: style.fontSize,
							// opacity: 1,
							// transition: 'opacity 0.5s',
							// transitionDelay: `${start}s`,
						}}
					>
						{text}
					</div>
				);
			})}
		</div>
	);
};

export default TextStream;
