import React from 'react';
import {staticFile, useVideoConfig, Audio} from 'remotion';
import audioSequences from './Assets/AudioSequences.json';
export default function AudioStream() {
	const {fps} = useVideoConfig();
	return (
		<>
			{audioSequences.map((entry, index) => {
				return (
					<Audio
						key={index}
						endAt={entry.props.endAt}
						startFrom={entry.props.startFrom}
						src={staticFile(entry.name)}
					/>
				);
			})}
		</>
	);
}
